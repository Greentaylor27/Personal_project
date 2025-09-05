import { prisma } from "../db/client";

export async function getUserById(id: bigint) {
  return prisma.users.findUnique({
    where: { id },
  })
}

export async function addUser(id: bigint, name: string) {
  return prisma.users.create({
    data: { id, name}
  });
}

export async function updateUser(id: bigint, newName: string) {
  return prisma.users.update({
    where: { id },
    data: { name: newName},
  })
}

export async function getRandomQuestion() {
  const rows = await prisma.questions.count();
  const skip = Math.floor(Math.random() * rows)

  const [question] = await prisma.questions.findMany({
    take: 1,
    skip,
  });
  return question
}
