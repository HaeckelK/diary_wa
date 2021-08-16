# Articles Service

## Development

## Launching

## Database
Initial setup of database required:
```bash
docker-compose exec articles-api bash
python3 -c "from app import db; db.create_all();"
```

## Future
This service should be removed from this repository, with endpoint contracts maintained.