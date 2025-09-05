import "dotenv/config";
import { Client, GatewayIntentBits } from "discord.js";
import { prisma } from "./db/client";
import wyrCommand from "./commands/wyr";
import { me } from "./commands/me";

// Discord client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ]
});

client.once("clientReady", () => {
  console.log(`✅ Logged in as ${client.user?.tag}`);
})

client.on("messageCreate", async (message) =>{
  if (message.author.bot) return;

  if (message.content === "!me") {
    await me(message);
  }

  if (message.content === "!wyr") {
    await wyrCommand(message);
  }
});

process.on("SIGINT", async () => {
  console.log("Shutting Down...");
  await prisma.$disconnect();
  client.destroy();
  process.exit(0);
});

client.login(process.env.DISCORD_TOKEN);
