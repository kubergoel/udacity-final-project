FROM postgres:13


# Copy the requirements file into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose port (Flask default is 5000)
EXPOSE 5432

