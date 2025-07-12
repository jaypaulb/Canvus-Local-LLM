# Changelog

## v1.3 proposed based on found undocumented api calls

- Added:
  - Annotations API
  - Canvas Backgrounds API
  - Color Presets API
  - Connectors API
  - Mipmaps API
  - Video Inputs API
  - Video Outputs API

## v1.2

- Added unauthenticated access for link-shared canvases and `link_permission` attribute to the `permissions` endpoint.
- Added `/uploads-folder` endpoint.
- Added `/send-test-email` endpoint.
- Added `title` parameter for Notes.
- Filter out the ID of the currently open canvas in the Client API if the user who makes the request doesn't have access to that canvas.
- Added `server_name` attribute to the `/server-config`.

## v1.1

- Removed `ini` file tokens, made authentication mandatory for most endpoints.
- Added `/login`, `login/saml` and `/logout` endpoints.
- Added users and groups management API.
- Added `/permissions` endpoints for canvases and folders.
- Added DELETE `/children` for folders.
- Added `mode` (demo or normal) attribute for canvases.
- Added `/save` and `/restore` endpoints for canvases.
- Added `/preview` for canvases.
- Added API tokens management API.
- Added license management API.
- Added audit log API.
- Added `/server-config` endpoint.
- Applied permissions model to the Client API.
- Added `/open-canvas` endpoint for workspaces.
- Added `user-email` and `server-id` attributes to the `/workspace`. 