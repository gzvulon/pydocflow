@Library("jenlib@master") _
// ===== /SHARED PART ====

// --- globas vars ---
def jg = [
    scmvars: null,
    node_label: 'mlg-cpu',
    cmds: [],
    tstages: [:],
    prj_dir: '.',
    commits: [],
    params: [
        samle: 'yes'
    ]
]

def add_stages(jg, filename, prefix){
    // echo "Load tasks from ${filename}"
    // filename='Taskfile.yml'
    def taskfile = readYaml file: filename
    for ( e in taskfile['tasks'] ) {
        jg.tstages[prefix + e.key] = e.value
        // echo "adding ${prefix}${e.key}"
    }
    echo "Loaded tasks from ${filename}"
    return taskfile
}


def step_stages_from_tasks(jg, wd, filename, root_job){
    // create piple stages from task commands
    def taskfile = add_stages(jg, filename, '')
    echo 'create stages from tasks'
    stage_names = []
    jg.cmds = taskfile['tasks'][root_job]['cmds']
    for (int i = 0; i < jg.cmds.size(); i++) {
        def _cmd = jg.cmds[i]
        def name = ""
        def cmd = ""
        try {
            name = _cmd['task']
            cmd = "task ${name}"
        }
        catch(Exception e) {
            name = _cmd
            cmd = _cmd
        }
        stage(name){
            dir(wd){
                sh cmd
            }
        }
    }
}
 // ===== /SHARED PART ====
// node(jg.node_label) {
node() {
timestamps {

    stage('fetch'){
        echo 'Fetch source'
        def scmvars = checkout scm
        def more = "repo_validate"
        jen.set_build_name(currentBuild, scmvars, more)
        jg['scmvars'] = scmvars
    }

    stage('commits'){
        jen.desc_from_commits(currentBuild, jg)
    }

    catchError {
        dir('apps/jentask'){
            step_stages_from_tasks(jg, jg.prj_dir, 'Taskfile.yml', 'ci-build')
        }
    }

   //  stage('finish'){
   //      def test_passed = readFile "build_info/tests_passed_report.txt"
   //      test_passed = test_passed.replace('passed', 'ok').replace('warnings', 'warn').replace('seconds', 's')
   //      def total_cov = readFile "build_info/coverage_total.txt"
   //      def commits = jg.commits.join(", ")
   //      jg.desc = "tests: ${test_passed}\n<br>coverage: ${total_cov}\n<br>commits: ${commits}"
   //      currentBuild.description = jg.desc
   //      junit 'coverage_html_report/*.junit.xml'
   //      archiveArtifacts 'coverage_html_report/*.junit.xml, build_info/*.txt'
   //      publishHTML (target: [
   //          allowMissing: false,
   //          alwaysLinkToLastBuild: false,
   //          keepAll: true,
   //          reportDir: 'coverage_html_report',
   //          reportFiles: 'index.html',
   //          reportName: "RCov Report"
   //      ])
   //  }
}}
