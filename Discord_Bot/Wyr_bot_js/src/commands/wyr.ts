import { Message, EmbedBuilder, bold } from "discord.js";
import { getRandomQuestion } from "../utils/db_utils";

export default async function wyr(message: Message) {
  try {
    const question = await getRandomQuestion();

    if (!question) {
      if (message.channel.isSendable()) {
        await message.channel.send("Couldn't find a Question at the moment please try again later!");
      }
      return;
    }

    const embed = new EmbedBuilder()
      .setTitle("🤔 Would You Rather?")
      .setDescription(`Would you Rather\n${question.option_a} ${bold("OR")}${question.option_b}`)
      .addFields(
        {name: "🇦 Option A", value: question.option_a, inline: true},
        {name: "🇧 Option B", value: question.option_b, inline: true}
      )
      .setColor("Random")
      .setFooter({ text: "Voting using the emojis below (only one vote is counted and random reactions won't be counted)"})

    if (!message.channel.isSendable()) return;
    const sentMessage = message.channel.send({ embeds: [embed] });

    (await sentMessage).react("🇦");
    (await sentMessage).react("🇧");

    
  } catch (err) {}
}
