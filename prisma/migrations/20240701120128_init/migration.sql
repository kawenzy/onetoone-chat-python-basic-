-- CreateTable
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "token" TEXT
);

-- CreateTable
CREATE TABLE "Chats" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "sendID" INTEGER NOT NULL,
    "receiverId" INTEGER NOT NULL,
    "msg" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Chats_sendID_fkey" FOREIGN KEY ("sendID") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
