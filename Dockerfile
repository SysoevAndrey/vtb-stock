FROM python:3.10-buster

ARG TARGET_APP
ARG TARGET_ALEMBIC_APP

ENV TARGET_APP=${TARGET_APP} \
    TARGET_ALEMBIC_APP=${TARGET_ALEMBIC_APP}

# Build system dependency
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Copy alembic configuration
COPY v3/src/alembic.ini /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy project code
COPY v3/src/${TARGET_APP} /code/${TARGET_APP}
COPY v3/src/shared_kernel /code/shared_kernel

# Copy initializer script
COPY v3/src/${TARGET_APP}/scripts/run-container.sh .
RUN chmod +x run-container.sh

CMD [ "./run-container.sh" ]
