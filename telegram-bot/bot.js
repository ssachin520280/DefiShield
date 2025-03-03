require("dotenv").config();
const TelegramBot = require("node-telegram-bot-api");

const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

bot.on("message", (msg) => {
    const chatId = msg.chat.id;
    const messageText = msg.text;

    if (messageText === "/start") {
        bot.sendMessage(chatId, "Welcome to the bot on new app!");
    }
});
