using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Frontend_bot.Bots
{
    public class EchoBot : ActivityHandler
    {
        // ✅ Static HttpClient with custom timeout (3 minutes)
        private static readonly HttpClient httpClient;

        static EchoBot()
        {
            httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromMinutes(5) // You can increase this if needed
            };
        }

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            try
            {
                var userQuestion = turnContext.Activity.Text;
                var apiUrl = "http://Localhost:8000/ask"; // FastAPI endpoint

                var requestData = new { question = userQuestion };
                var json = JsonConvert.SerializeObject(requestData);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await httpClient.PostAsync(apiUrl, content);
                var responseContent = await response.Content.ReadAsStringAsync();


                if (response.IsSuccessStatusCode)
                {
                    var result = JObject.Parse(responseContent);
                    string answer = result["answer"]?.ToString();

                    await turnContext.SendActivityAsync(MessageFactory.Text(answer), cancellationToken);
                }
                else
                {
                    string errorMsg = $"⚠ API Error: {response.StatusCode} - {responseContent}";
                    await turnContext.SendActivityAsync(MessageFactory.Text(errorMsg), cancellationToken);
                }
            }
            catch (Exception ex)
            {
                await turnContext.SendActivityAsync(MessageFactory.Text("🚨 Error: " + ex.Message), cancellationToken);
            }
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            var welcomeText = "Hello and welcome! Ask me anything about the Cati organization";
            foreach (var member in membersAdded)
            {
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText), cancellationToken);
                }
            }
        }
    }
}
