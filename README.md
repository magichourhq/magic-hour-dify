# Magic Hour for Dify

Generate AI images and videos from Dify agents and workflows with the [Magic Hour API](https://docs.magichour.ai/). The plugin uploads Dify image inputs, starts asynchronous generation jobs, and retrieves completed project results without creating duplicate paid jobs.

## Tools

- **Create image** starts an AI Image Generator job and returns its project ID and charged credits.
- **Create video** starts a Text-to-Video job and returns its project ID and charged credits.
- **Animate image** uploads a Dify image, starts an Image-to-Video job, and returns its project ID and charged credits.
- **Get image project** returns current status and emits completed images when available.
- **Get video project** returns current status and signed video download links when available.

Generation is asynchronous. Keep the project ID returned by a create tool and pass that same ID to the matching get tool. A queued or rendering status is not a failed job; wait and retrieve it again. Do not repeat a create call to recover a polling delay because a second call creates another paid job.

## Configure

1. Create a Magic Hour API key at [magichour.ai/developer](https://magichour.ai/developer?tab=api-keys).
2. Install the packaged `.difypkg` in Dify or run the plugin in Dify's remote debug mode.
3. Enter the API key in the plugin's **Magic Hour API key** field. Dify stores it as a secret provider credential.
4. Add a create tool and its matching get tool to an agent or workflow.

Image and video generation consumes Magic Hour credits. The plugin validates credentials with `GET /v1/account`; it does not expose account details to workflows during setup.

## Develop and package

Requires Python 3.12 and the [Dify plugin CLI](https://docs.dify.ai/plugins/quick-start/develop-plugins/initialize-development-tools).

```sh
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m main
```

From the repository's parent directory, package a reviewed build:

```sh
dify-plugin plugin package ./magic-hour-dify
```

Marketplace publication is a separate reviewed submission to [`langgenius/dify-plugins`](https://github.com/langgenius/dify-plugins).

## Privacy

See [PRIVACY.md](PRIVACY.md).
