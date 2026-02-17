export $(grep -v '^#' .env.example | xargs)
cp .env.example .env
