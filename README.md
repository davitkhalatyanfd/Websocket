WebSocket Moon Server

This project is a WebSocket server that provides the Right Ascension (RA) and Declination (Dec) coordinates of the Moon every 10 seconds. The RA and Dec values are calculated independently without using external astronomical libraries. The server is made publicly accessible via Ngrok, allowing real-time testing using online WebSocket tools.


Features:

Implements a WebSocket server using websockets.

Computes RA and Dec values based on a simplified lunar model.

Updates Moon coordinates every 10 seconds.

Publicly accessible via Ngrok for external connections.


Prerequisites:

Make sure you have Python installed (>= 3.7) along with the required dependencies:

pip install websockets pyngrok


Running the WebSocket Server:

Clone the repository:
git clone https://github.com/yourusername/websocket-moon-server.git
cd websocket-moon-server


Start the WebSocket server:
python websocket_moon_server.py

Copy the Ngrok public WebSocket URL from the terminal output.

Use an online WebSocket client (e.g., PieSocket) to connect and receive real-time Moon coordinates.


Example Output:

WebSocket public URL: ws://random-ngrok-url.ngrok.io
Moon RA: 05:43:12.45, Dec: -23.456°
Moon RA: 05:44:02.12, Dec: -23.470°
