pipeline {
  agent {
    kubernetes {
      yaml """
      apiVersion: v1
      kind: Pod
      metadata:
      spec:
        containers:
        - name: kaniko
          image: 'gcr.io/kaniko-project/executor:debug'
          command:
          - sleep
          args:
          - infinity
        - name: helm
          image: 'mirror.gcr.io/alpine/helm'
          command:
          - sleep
          args:
          - infinity
        - name: git
          image: 'alpine/git:latest'
          command:
          - sleep
          args:
          - infinity
        restartPolicy: Never
      """
    }
  }
  environment {
    APP_NAME = "api-key-manager"
    RELEASE = "1.0.0"
    HARBOR_REGISTRY = "192.168.1.200:30002"
    HARBOR_PROJECT = "ivansanmartin"
    HARBOR_USERNAME = credentials('harbor-username')
    HARBOR_PASSWORD = credentials('harbor-password')
    IMAGE_NAME = "${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${APP_NAME}"
    IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
    GIT_URL = "https://github.com/ivansanmartin/api-key-manager"
    HELM_CHART_PATH = "./k8s"
    NAMESPACE = "ivansanmartin"
    RELEASE_NAME = "api-key-manager"
  }
  
  stages {
    stage("Cleanup Workspace") {
      steps {
        cleanWs()
      }
    }
    
    stage("Checkout from SCM") {
      steps {
        container('kaniko') {
          checkout([$class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[url: "${GIT_URL}", 
                                         credentialsId: 'jenkins-github']]
          ])
        }
      }
    }
    
    stage('Configure Docker Auth') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''#!/busybox/sh
            mkdir -p /kaniko/.docker
            chmod 777 /kaniko/.docker
            echo '{"auths":{"192.168.1.200:30002":{"username":"'"${HARBOR_USERNAME}"'","password":"'"${HARBOR_PASSWORD}"'"}}}'  > /kaniko/.docker/config.json
            ls -la /kaniko/.docker/
            cat /kaniko/.docker/config.json
          '''
        }
      }
    }
    
    stage('Build & Push with Kaniko') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''#!/busybox/sh
            /kaniko/executor \
              --dockerfile `pwd`/Dockerfile \
              --context `pwd` \
              --destination=${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${APP_NAME}:${IMAGE_TAG} \
              --destination=${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${APP_NAME}:latest \
              --insecure \
              --insecure-pull \
              --skip-tls-verify \
              --verbosity=debug
              
          '''
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        container('helm') {
          script {
            sh """
              helm upgrade --install ${APP_NAME} ${HELM_CHART_PATH} \
                --namespace ${NAMESPACE} \
                --set image.repository=${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${APP_NAME} \
                --set image.tag=${IMAGE_TAG} \
                --wait \
                --timeout 5m
            """
          }
        }
      }
    }

  }
}