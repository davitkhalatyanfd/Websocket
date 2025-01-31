import asyncio
import websockets
from pyngrok import ngrok
import math
from datetime import datetime


def julian_date():
    now = datetime.utcnow()
    year, month, day = now.year, now.month, now.day
    hour, minute, second = now.hour, now.minute, now.second

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    JD += (hour + minute / 60 + second / 3600) / 24
    return JD


def calculate_moon_position():
    JD = julian_date()
    D = JD - 2451545.0  # Days since J2000.0

    L = (218.316 + 13.176396 * D) % 360  # Mean longitude
    M = (134.963 + 13.064993 * D) % 360  # Mean anomaly
    F = (93.272 + 13.229350 * D) % 360  # Moon's argument of latitude

    lambda_moon = L + 6.289 * math.sin(math.radians(M))
    beta_moon = 5.128 * math.sin(math.radians(F))
    epsilon = 23.439 - 0.0000004 * D  # Obliquity of the ecliptic

    lambda_rad, beta_rad, epsilon_rad = map(math.radians, [lambda_moon, beta_moon, epsilon])

    RA = math.atan2(math.cos(epsilon_rad) * math.sin(lambda_rad), math.cos(lambda_rad))
    Dec = math.asin(
        math.sin(beta_rad) * math.cos(epsilon_rad) + math.cos(beta_rad) * math.sin(epsilon_rad) * math.sin(lambda_rad))

    RA_deg = math.degrees(RA) % 360 / 15  # Convert degrees to hours
    Dec_deg = math.degrees(Dec)

    RA_h = int(RA_deg)
    RA_m = int((RA_deg - RA_h) * 60)
    RA_s = ((RA_deg - RA_h) * 60 - RA_m) * 60
    RA_str = f"{RA_h:02}:{RA_m:02}:{RA_s:05.2f}"

    return RA_str, Dec_deg


async def broadcast_moon_position(websocket):
    try:
        while True:
            RA, Dec = calculate_moon_position()
            message = f"Moon RA: {RA}, Dec: {Dec:.3f}°"
            await websocket.send(message)
            await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def websocket_server():
    server = await websockets.serve(broadcast_moon_position, "localhost", 8080)
    tunnel = ngrok.connect(8080, "http")
    print(f"WebSocket public URL: {tunnel.public_url.replace('http', 'ws')}")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(websocket_server())
