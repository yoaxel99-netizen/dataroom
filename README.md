Technology Stack
	1. Backend: Python, Django, PostgreSQL
	2. Frontend: ReactJS
	3. Security: oAuth

GENERAL Questions
		- to be tackled along the way
		- will have an answer written in the roadmap or tech stack or somewhere else (these will dissapear)

	Technologies that could be used for security?
		- X-Accel-Redirect header -> handle the file serve on the webserver layer, keep access/permissons and logic for the backend

	File persistence:
		- save directly to a folder on the server, outside the containers? -> needs mapping at docker-compose.yaml level and nginx/caddy level (webserver config file)

Roadmap:
	1. Setup local dev env Python/Django project "dataroom" + PSQL DB (DONE)
	2. Install and integrate the frontend layer with NextJS (DONE)
		- install packages, then configure for local env use (DONE)
		- create (or use from demos) a simple page for test (DONE)
		- "connect" an endpoint which can be used to populate data into the frontend page (DONE)
	3. Integrate oAuth library into Python/Django to connect our app to Google Drive (develop the UI flow to connect Google Drive) (DONE)
	4. Design the foundation (basics) for the domain model (DONE)
	5. Design the foundation (basics) for the data model (DONE)
	6. DRF (django rest framework) to build REST API endpoints for NextJS frontend (80% DONE)
	7. Create the frontend single page application with Google Drive File Picker (WIP)

After everything works perfect on local env:
	1. Test edge cases (direct URL GET, no authentication, expired oAuth token, tampered auth token from Postman)
	2. Containerize the technologies (configure docker, dockerfile, docker-compose.yaml, caddyfile, makefile)
	3. Deploy the solution to test the "live" app
	4. Test server shutdowns, restarts, manual crashes to analyse app's reliability
	5. Construct the README file with precise step-by-step actions to install/configure/use the product locally (preferrably 2 ways: just local technologies; containarized technologies)

*********************************************************************************************************************************************************************
CLIENT Goals
	1. Robustness, scalability and security
	2. User experience and functionality
	3. Code quality and readability


CLIENT Functional requirements - CRUD operations
	File Management:
		- Import files from Google Drive into dataroom
		- View file list in UI
		- Click on file to view in browser
		- Delete a file imported into Dataroom (not in Google drive)

	(Optional) For extra credit:
		- You can add an authentication layer using social auth or user/password
		- You can add search and filtering features that allows users to search for documents based on contents or file names.


CLIENT Technical Requirements (translate this to domain model - business logic)
	Frontend:
		- Users go through a UI flow to authenticate with google drive
		- Users can select files on the UI to import
			INFO: you may use google drive file picker out of the box or create your own picker
		- Users are allowed to import files from Google Drive in the UI, and these are displayed in UI

	Backend:
		- Store metadata in a DB to persist files and application state across page refreshes and user sessions. You can use any DB
		- Store oauth tokens and persist files on server disk (no need to use blob etc)


CLIENT Pointers / What to think of when designing the app:
	- Good data model design to support functional requirements
	- Handle OAuth and token storage in backend
	- Clean and intuitive UI/UX
	- Edge cases, ex: using an expired oAuth token
*********************************************************************************************************************************************************************