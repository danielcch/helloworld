pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                echo "Hacemos Checkout"
                git 'https://github.com/danielcch/helloworld.git'
            }
        }
        stage('Build') {
            steps {
                echo "Etapa construccion: No se compila nada de monto en python"
            }
        }
        stage('Test') {
            parallel{
                stage('Unit') {
                    steps {
                        sh '''
                            export PYTHONPATH=.
                            export FLASK_APP=app/api.py:api_application
                            pytest --junitxml=result-unint.xml test/unit
                        '''
                    }
                }// fin Unit
                stage('Service') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export PYTHONPATH=.
                                export FLASK_APP=app/api.py:api_application
                                
                                PORT_FLASK=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
                                PORT_WIREMOCK=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
                                
                                flask run --port=$PORT_FLASK &
                                FLASK_PID=$!
                                
                                java -jar /tools/wiremock/wiremock-standalone-2.27.2.jar --port $PORT_WIREMOCK --root-dir /tools/wiremock/ -v &
                                WIREMOCK_PID=$!
                                
                                trap 'kill $FLASK_PID $WIREMOCK_PID || true' EXIT
                                
                                for i in {1..100}; do curl -s http://localhost:$PORT_FLASK && break || sleep 1; done
                                for i in {1..100}; do curl -s http://localhost:$PORT_WIREMOCK && break || sleep 1; done
                                
                                export BASE_URL_ENV=http://localhost:$PORT_FLASK
                                export BASE_URL_MOCK_ENV=http://localhost:$PORT_WIREMOCK
                                
                                pytest --junitxml=result-unint-rest.xml test/rest
                            '''
                        }
                    }
                } //fin Service
            }// fin parallel
        }// fin Test
        stage ('Results') {
            steps {
                junit 'result*.xml'
            }
        }
    }//fin stages
}
