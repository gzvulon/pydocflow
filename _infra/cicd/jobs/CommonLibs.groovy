// === Job DSL jobs declarations ===

// ----------------------------------------------------
// --- Parameters And Defaults ---

def g = [:]
g.credentials = "********-****-****-****-************"
g.activeBranches = ["master dev"]
g.buildsToKeep = 20

// ----------------------------------------------------
// --- Jobs Dsl ---

multibranchPipelineJob('YD/LIBS/libstore') {
    description('Packages are distributed to <a href="http://packages:8081/packages">http://packages:8081/packages</a>')
    triggers {
        periodic(1)
    }
    factory {
        workflowBranchProjectFactory {
            scriptPath('libs/libstore/Jenkinsfile')
        }
    }
    branchSources {
        git {
            remote('git@github.com:gzvulon/pydocflow.git')
            credentialsId(g.credentials)
            includes(g.activeBranches)
            id('YD-LIBS-libstore-pydocflow')

        }
    }
    orphanedItemStrategy {
        discardOldItems {
            numToKeep(g.buildsToKeep)
        }
    }
}
