# Stage 1
FROM node:18-alpine as builder

WORKDIR /vue_app

# Copy package.json 
COPY ./vue_app/package*.json ./
# Install node dependencies
RUN npm install

COPY ./vue_app/ .

# Build the project
RUN npm run build

# Stage 2
FROM nginx:alpine as production

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from stage 1
COPY --from=builder /vue_app/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
