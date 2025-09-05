import { Message } from "discord.js";
import { getUserById } from "../utils/db_utils";

export async function me(message: Message) {
  console.log("Beginning looking for a user");

  const user = BigInt(message.author.id)
  const foundUser = await getUserById(user);

  console.log("May have found a user!");
  const channelId = message.channel.id;


  if (foundUser) {
    console.log("Found a user!")
    if (message.channel.isSendable()) {
      await message.channel.send(`Hello, ${foundUser.name} Glad you could make it here`);
    } else {
      console.error("Channel not sendable:", channelId);
    }
  } else {
    if (message.channel.isSendable()) {
      await message.channel.send("You're not in the database, YET!!!");
    } else {
      console.error("Channel not sendable:", channelId);
    }
  }
}
