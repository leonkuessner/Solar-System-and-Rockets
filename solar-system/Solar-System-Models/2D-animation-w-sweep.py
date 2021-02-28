import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

df = pd.read_csv("data3.csv")

df["semiMinorAxis"] = df["semiMajorAxis"]*np.sqrt(1-df["ecc"]**2)

wanted_planets = "innerPlanet"
min_planet = 6
max_planet = 12
time_pf = 30  # In DAYS
# multiple = 5


itera = 0


def plotLines(i):
    theta = np.linspace(0, 2*np.pi, 500)

    r = (df["semiMajorAxis"][i]*(1-df["ecc"][i]**2) / (1-df["ecc"][i]
                                                       * np.cos(theta)))  # radius = a(1-Eps^2)/(1-Eps*cosTheta)
    # r = (df["a"][i]*(1-df["Epsilon"][i]**2)) / \
    #     (1+df["Epsilon"][i]*np.cos(Ttheta))
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    ax.plot(x, y)


def getValues(i, Ttheta, dTime, area):
    P = df["P_orb"][i]*365.256   # How many days a rotation takes
    r = (df["semiMajorAxis"][i]*(1-df["ecc"][i]**2) / (1-df["ecc"][i]
                                                       * np.cos(Ttheta)))  # radius = a(1-Eps^2)/(1-Eps*cosTheta)
    # r = (df["a"][i]*(1-df["Epsilon"][i]**2)) / \
    #     (1+df["Epsilon"][i]*np.cos(Ttheta))
    x = r*np.cos(Ttheta)
    y = r*np.sin(Ttheta)
    dTheta = ((2*area*dTime)/(P*r**2))
    # if i == 11:
    #     print(Ttheta)
    return x, y, dTheta


def update(i, xData, yData):
    planetsX = []
    planetsY = []

    time_c = time_pf

    # print(i, len(xArr), i % len(xArr))
    years = round(1000*i*time_c/365.256)/1000

    for j in range(max_planet-min_planet):
        t = i
        if t >= len(xData[j]):
            t = i % len(xData[j])
        planetsX.append(xData[j][t])
        planetsY.append(yData[j][t])

    planets.set_data(planetsX, planetsY)
    title.set_text(u"Years: {}".format(years))
    return planets, title,


plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 10))

planets, = ax.plot([], [], '.', markersize=11, c='w')
title = ax.text(0.5, 0.97, "", bbox={'facecolor': 'w', 'alpha': 0.0, 'pad': 5},
                transform=ax.transAxes, ha="center")


ax.plot(0, 0, 'X', markersize=5, color="yellow")

xData = []
yData = []

for i in range(min_planet, max_planet):
    plottingLines = plotLines(i)
    Ttheta = 0
    area = np.pi*df["semiMajorAxis"][i] * \
        df["semiMinorAxis"][i]  # Area of ellipse = pi*a*b
    # print(Ttheta)
    xArr = []
    yArr = []
    while Ttheta < 2*np.pi:
        # print(Ttheta)
        # Updating every 2 hours
        x, y, dTheta = getValues(i, Ttheta, time_pf, area)
        xArr.append(x)
        yArr.append(y)
        Ttheta = Ttheta+dTheta
    xData.append(xArr)
    yData.append(yArr)

    # ax.plot(xArr, yArr)

    planets.set_data(xArr[0], yArr[0])
# print(xArr[571])
anim = FuncAnimation(fig, update, interval=1,
                     blit=True, fargs=(xData, yData))
# anim = FuncAnimation(fig, update, interval=1, blit=True, fargs=(xArr, yArr))

# ax.set_xlim([-80, 80])
# ax.set_ylim([-80, 80])

plt.gca().set_aspect('equal', adjustable='box')

ax.grid(True, lw=0.1)
plt.show()


# plt.plot(xVals, yVals)

# print(f"area of planet {planet}:", area)
# print(f"r of planet {planet}:", r)
# print(f"dTheta of planet {planet}:", dTheta)

# print(0.04109*np.pi/180)
