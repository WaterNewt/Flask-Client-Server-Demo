# Flask Client-Server Game Demo

Flask Client-Server Game Demo is a simple, yet innovative project that highlights the versatility of Flask in facilitating server-client communication. Serving as a comprehensive guide to building robust game servers, this project equips users with the knowledge and skills necessary to develop scalable network architectures. Through hands-on experimentation, participants can explore the intricacies of Flask's routing system, HTTP methods, and data exchange protocols.

## Setup

#### Install Dependencies:
When you're in the project directory, run `pip3 install -r requirements.txt`, this command will install all the required dependencies to run the scripts.

### Running the server:
To run the server, run `python3 server.py`, this command will start the Flask server in port `8000`

### Running the client:
To run the client, run `python3 client.py 127.0.0.1:8000 user`, if the server is not running on your local network, you must change `127.0.0.1:800` with the public IP and the port that the server is running on. You may replace the `user` with any username you like, if the username is not in the database (`world.bson`), it will add it to the database automatically. This will open a pygame window with a square as your player, the controls are <b>left arrow key, right arrow key, up arrow key and down arrow key.</b> You may not open multiple games as the same user, this will give you an error.

## Contributing
Feel free to contribute to this repository! But please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and the [Contributing](CONTRIBUTING.md) guides.

## License
This project is under the GPL 3 license. Read more [here](LICENSE)