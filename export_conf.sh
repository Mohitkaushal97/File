# usage: source export_conf.sh
export API__SERVER_WITH_PORT=`heroku config:get API__SERVER_WITH_PORT`
export SECRET_AUTH__JOBS_APP_SECRETS=`heroku config:get SECRET_AUTH__JOBS_APP_SECRETS`
export DJANGO_SETTINGS_MODULE=`heroku config:get DJANGO_SETTINGS_MODULE`
export DATABASE_URL=`heroku config:get DATABASE_URL`

if [ -z "$API__SERVER_WITH_PORT" ]
then
	echo "\$API__SERVER_WITH_PORT is empty! set it in heroku config and run \"source export_conf.sh\" again"
fi

if [ -z "$SECRET_AUTH__JOBS_APP_SECRETS" ]
then
	echo "\$SECRET_AUTH__JOBS_APP_SECRETS is empty! set it in heroku config and run \"source export_conf.sh\" again"
fi
