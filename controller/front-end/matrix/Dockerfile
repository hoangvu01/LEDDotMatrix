# Official LTS image from NodeJS
FROM node:current-slim

# Set working directory
WORKDIR /usr/src/app

# Copy files to container
COPY package* ./ 

# Run command
RUN npm install
RUN npm install react-scripts@3.4.1 --silent

# Copy rest of folder
COPY . ./

# Execute
CMD ["npm", "run",  "start"]

