pipeline {
agent any
stages {

    stage('Create') { steps {
        echo 'Create World'
        jobDsl scriptText: (
'''pipelineJob('example5') {
    definition {
        cps {
            script(
"""
pipeline {
   agent any
   stages {
      stage('Hello') { steps {
        echo 'Hello World'
        sh 'ls -alh'
        sh 'pwd'
        sh "docker version || echo '[NOT_INSTALLED=docker]'"
      }}
      stage('GoodBye') { steps { script {
          currentBuild.description = 'bla'
      }}}
   }
}
""")
            // sandbox()
        }
    }
}''')
    }}
}}
