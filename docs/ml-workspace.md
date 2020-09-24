# ML Workspace

```bash
 docker run -d \
    -p 80:8080 \
    --name "ml-workspace" -v "${PWD}:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="OH:mytoken" \
    --shm-size 512m \
    --restart always \
    dagshub/ml-workspace:latest
```
