<h1>Multi-objective Resource Capacity Planning Optimizer for Call Center
</h1>
This Optimization tool is a calculator that allows to optimize the workforce at the call center:
1. Punctual forecast calculates the number of agents needed to handle a specific workload.
2. Punctual Reverse Forecast calculates the maximum number of calls/request available agents can handle.
3. Multi-Objective Forecast calculates the number of agents needed to handle a specific workload considering multiple languages, channels for a specific time frame.

<h3>How to run the project using docker:</h3>
<h4>Pre-requisites:</h4>
<p>Docker https://docs.docker.com/engine/install/ubuntu/</p>
<p>Docker compose: https://docs.docker.com/compose/install/</p>

<h4>Create .env file in the project directory like this:</h4>
`export POSTGRES_PASSWORD="password"
export POSTGRES_USER="postgres_user"
export DB_NAME="wfm"
export MAILGUN_USER="user@mailgun.org"
export MAILGUN_PSSWORD="mailgun_password"`

<p>Mailgun credentials are optional and needed for reset password only</p>


<h3>Please run the comments below from the project directory</h3>
<h4>Build containers:</h4>
`docker compose build`

<h4>Apply database migrations:</h4>
`docker compose run app python manage.py migrate`

<h4>Run the project:</h4>
`docker compose up`
