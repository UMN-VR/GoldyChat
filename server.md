# Server.js Overview

`server.js` is a Node.js server application for handling various web browsing tasks. The server is built on Express, a minimalist web application framework for Node.js. It also uses Puppeteer, a headless Chrome Node.js API, to control a Chromium or Chrome browser.

The server is primarily responsible for the following tasks:

1. **Starting the Browser:** The server starts a new browser instance when it receives a GET request at the `/start` endpoint. It uses Puppeteer's `launch` function to start a Chromium browser. The server responds with a message indicating that the browser has been started.

2. **Opening URLs:** The server can open a new tab in the browser and navigate to a specified URL. This is done when it receives a GET request at the `/openURL` endpoint with a URL as a parameter. The server creates a new page with Puppeteer's `newPage` function and navigates to the URL with the `goto` function. The server responds with a message indicating that the URL has been opened and the ID of the new page.

3. **Taking Screenshots:** The server can take screenshots of a webpage. When it receives a GET request at the `/takeScreenshot` endpoint with a page ID as a parameter, it takes a screenshot of the specified page with Puppeteer's `screenshot` function. The server responds with a message indicating that the screenshot has been taken and the path of the screenshot image file.

4. **Closing Tabs:** The server can close a browser tab when it receives a GET request at the `/closeTab` endpoint with a page ID as a parameter. It closes the specified page with Puppeteer's `close` function and removes the page from its record. The server responds with a message indicating that the tab has been closed.

5. **Taking Screenshots and Closing Tabs:** The server can also navigate to a URL, take a screenshot, and close the tab in one operation. This is done when it receives a GET request at the `/screenshot` endpoint with a URL as a parameter.

The server listens on port 3000 for incoming requests.

Please remember to install the required Node.js packages (express and puppeteer) by running `npm install` in the directory containing `server.js`. You also need to have Chromium or Chrome installed on the system, and the path to the browser executable should be correctly specified in the `launch` function call.
