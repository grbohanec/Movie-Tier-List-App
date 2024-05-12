FROM nginx:latest

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy a configuration file from the current directory
COPY nginx.conf /etc/nginx/conf.d/

