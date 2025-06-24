import time
import numpy as np
import random
import math
import matplotlib.pyplot as plt

class Knapsack_PSO():

    def __init__(self, data, maxKnapsack, iterasi, pop_size):
        self.pop_size = pop_size
        self.data = data
        self.iterasi = iterasi
        self.c1 = 2
        self.c2 = 2
        self.w = 0.1
        self.maxKnapsack = maxKnapsack
        self.dataConvert = []
        self.vMin = -1
        self.vMax = 1
        self.treshold = 0.5
        self.gBest = [None, None]
        self.fitnesspBest = []
        self.history = []
        self.initial()

    def initial(self):
        for i in range(self.pop_size):
            temp = []
            mutasi = ''
            for j in self.data:
                randomBarangValue = round(random.random(), 3)
                binary = self.convertDataToBinary(randomBarangValue)
                particleVelocity = round( self.vMin + ( round(random.random(), 3) * ( self.vMax - self.vMin ) ) , 3)

                temp.append([randomBarangValue, binary, particleVelocity])
                mutasi += '0'

            self.fitnesspBest.append([0, mutasi])
            self.dataConvert.append(temp)

    def convertDataToBinary(self, data):
        if data > self.treshold:
            return 1
        else:
            return 0

    def updateVelocity(self, indPartikel, ind):
        r1 = round(random.random(), 1)
        r2 = round(random.random(), 1)
        print(f"\npartikel[{indPartikel+1},{ind+1}] : {self.dataConvert[indPartikel][ind]}")
        print(f"fitness dan pBest : {self.fitnesspBest[indPartikel]}")
        print(f"gBest : {self.gBest}")

        posisi = self.dataConvert[indPartikel][ind][1]
        v = self.dataConvert[indPartikel][ind][2]
        pBest = int(list(self.fitnesspBest[indPartikel][1])[ind])
        gBest = int(self.gBest[1][ind])

        print(f"v(i+1) = {self.w} * {v} + {self.c1} * {r1} * [{pBest} - {posisi}] + {self.c2} * {r2} * [{gBest} - {posisi}]")
        print(f"v(i+1) = {self.w * v} + {self.c1 * r1 * (pBest - posisi)} + {self.c2 * r2 * (gBest - posisi)}")
        vNext = (self.w * v) + (self.c1 * r1 * (pBest - posisi)) + self.c2 * r2 * (gBest - posisi)
        print(f"v(i+1) = {round(vNext, 3)}")
        return round(vNext, 3)

    def updatePosisi(self, x, v):
        print(f"x(i+1) = {x} + {v}")
        xNext = x + v
        print(f"x(i+1) = {x + v}")
        return round(xNext, 3)

    def fitness(self, dataPartikel):
        print('fitness')
        nilaiFitness = 0
        for i in range(len(dataPartikel)):
            print(f"{dataPartikel[i][1]} * {self.data[i][1]} = {dataPartikel[i][1] * self.data[i][1]}")
            nilaiFitness += (dataPartikel[i][1] * self.data[i][1])
        return nilaiFitness

    def updatePBest(self, ind, hasilFitness):
        if self.fitnesspBest[ind][0] < hasilFitness:
            print(f"karena pBest sekarang ({hasilFitness}) lebih besar dari sebelumnya ({self.fitnesspBest[ind][0]}), maka diupdate:")
            self.fitnesspBest[ind][0] = hasilFitness
            binary = ''
            for i in range(len(self.dataConvert[ind])):
                # print(self.dataConvert[ind][i][1])
                binary += str(self.dataConvert[ind][i][1])
            self.fitnesspBest[ind][1] = binary
        print(f"pBest -> {self.fitnesspBest[ind][1]}")

    def updateGBest(self, data):
        print('updateGBest')
        terbesar = [None, None]
        for i in data:
            if terbesar[0] == None or terbesar[0] < i[0]:
                terbesar[0] = i[0]
                terbesar[1] = i[1]
        self.gBest = terbesar
        print(f"gBest -> {self.gBest}")

    def cekPenalty(self, ind):
        print('cek penalty')
        print('perhitungan berat :')
        totalBerat = 0
        data = self.dataConvert[ind]
        for i in range(len(data)):
            print(f"{self.data[i][0]} * {data[i][1]} = {self.data[i][0] * data[i][1]}")
            if data[i][1] == 1:
                totalBerat += self.data[i][0]
        print(f"pBest -> {self.fitnesspBest[ind][1]}")
        print(f"total berat = {totalBerat}, knapsack = {self.maxKnapsack}")
        if totalBerat > self.maxKnapsack:
            self.fixPenalty(ind, totalBerat)
        else:
            print('tidak ada penalty')

    def fixPenalty(self, ind, totalBerat):
        print(f"penalty : melebihi kapasitas knapsack")
        while totalBerat > self.maxKnapsack:
            arr = []
            indices = []
            for i in range(len(self.dataConvert[ind])):
                arr.append(self.dataConvert[ind][i][1])
                if self.dataConvert[ind][i][1] == 1:
                    indices.append(i)
            print(f"binary -> {arr}", end=", ")
            print(f"index terdapat angka 1 -> {indices}")
            if indices != []:
                randomInd = random.choice(indices)
                print(f"terpilih index {randomInd}")
                arr[randomInd] = 0
                self.dataConvert[ind][randomInd][1] = 0
                print(f"binary baru -> {arr}")
            print(f"update penalty partikel ->  {self.dataConvert[ind]}")

            totalBerat = 0
            data = self.dataConvert[ind]
            for i in range(len(data)):
                if data[i][1] == 1:
                    totalBerat += self.data[i][0]
            print(f"total berat = {totalBerat}, knapsack = {self.maxKnapsack}")
            if totalBerat < self.maxKnapsack:
                break

    def run(self):
        self.history.append([0, [0, '']])
        # print(self.dataConvert[0][0][0])
        for i in range(self.iterasi):
            print(f"iterasi ke-{i+1}")
            print()
            # pBests = []
            for j in range(self.pop_size):
                # convert biner
                for k in range(len(self.dataConvert[j])):
                    self.dataConvert[j][k][1] = self.convertDataToBinary(self.dataConvert[j][k][0])

                print(f"partikel ke-{j+1}")
                print(self.dataConvert[j])

                # penalty
                self.cekPenalty(j)

                # fitness
                hasilFitness = self.fitness(self.dataConvert[j])
                print(f"hasil fitness -> {hasilFitness}")
                self.updatePBest(j, hasilFitness)
                print()

            # gBest
            print(f"kandidat gBest :")
            for j in range(len(self.fitnesspBest)):
                print(f"partikel ke-{j+1} : {self.fitnesspBest[j]}")

            self.updateGBest(self.fitnesspBest)

            self.history.append([i, self.gBest])

            for k in range(self.pop_size):
                for l in range(len(self.dataConvert[k])):

                    # update velocity
                    vNext = self.updateVelocity(k, l)
                    print(f"velocity lama : {self.dataConvert[k][l][2]}", end=", ")
                    self.dataConvert[k][l][2] = vNext
                    print(f"velocity baru : {vNext}")

                    # update posisi
                    xNext = self.updatePosisi(self.dataConvert[k][l][0], vNext)
                    print(f"posisi lama : {self.dataConvert[k][l][0]}", end=", ")
                    self.dataConvert[k][l][0] = xNext
                    print(f"posisi baru : {xNext}")

                    # detail update partikel
                    print(f"update partikel[{k+1},{l+1}] : {self.dataConvert[k][l]}")
                print()

# Format data : [Wi, Pi]
# fitnesspBest = [value, binary]
# dataConvert = [posisi, isSelected, velocity]

# partikel
# print(self.dataConvert[j])
# subPartikel
# print(self.dataConvert[j][0])
# print(self.dataConvert[j][1])
# print(self.dataConvert[j][2])
# print(self.dataConvert[j][3])
# print(self.dataConvert[j][4])

# 0 - posisi
# print(self.dataConvert[j][0][0])
# 1 - binary
# print(self.dataConvert[j][0][1])
# 2 - velocity
# print(self.dataConvert[j][0][2])