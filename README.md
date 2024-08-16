# Simple Watermark Generator

## Overview
The **Simple Watermark Generator** is a Python-based tool that allows you to add a transparent image as a watermark or a line of text to an image using Swagger. The project is designed to be safe and efficient, with no user interface, and can be run entirely offline within a Docker container. This ensures that your images remain on your local machine and are not exposed to the internet.

## Features
- **No UI, Just Swagger**: The tool is operated entirely through Swagger, making it straightforward to use.
- **Offline and Secure**: The containerized environment does not require internet access, ensuring that your images are processed securely.
- **Configurable Watermark Position**: You can specify the x and y coordinates to adjust the position of the watermark.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd simple-watermark-generator
   ```

2. Build the Docker container from the Dockerfile:

    ```bash
    docker build -t simple-watermark-generator .
    ```

3. Run the container:

    ```bash
    docker run -p 8000:8000 simple-watermark-generator
    ```

## Usage
- Create a watermark image with a transparent background in PNG format using an external tool.
- Access the Swagger interface at http://127.0.0.1:8000/docs#/.
- Upload the image and the watermark, configure the x and y positions, and execute the POST command to apply the watermark.


## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. For code contributions, fork the repository, create a branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Created by [Ivan Ajimura](https://github.com/ivanajimura).  
Connect with me on [GitHub](https://github.com/ivanajimura) and [LinkedIn](https://www.linkedin.com/in/ivanajimura/).
