# Change log of default runtime image
## Runtime image
In Azure Machine Learning prompt flow, runtime provides the environment to execute flows. The default runtime includes a pre-built Docker image, which contains all necessary dependent packages.

### Pull image
The image can be pulled by specifying a runtime version and executing the following command:
```
docker pull mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:<runtime_version>
```

### Check image version
You can check the runtime image version from the flow execution log:
![img](../../media/cloud/runtime-change-log/runtime-version.png)

## Change log
Default runtime image is continuously updated, and here we record the new features and fixed bugs of each image version.

### 20240411.v4

#### New features
- Add 'detail' parameter on 'Azure OpenAI GPT-4 Turbo with Vision" tool and "OpenAI GPT-4V" tool.

#### Bugs fixed
- Resolve an intermittent ImportError that arose while loading the package tool.
- Upgrade langchain>=0.1.1 and langchain-core>=0.1.30 to fix vulnerability.

### 20240403.v2

#### New features
NA

#### Bugs fixed
NA


### 20240326.v2

#### New features
- Support environment variables for C# batch run.

#### Bugs fixed
NA


### 20240319.v1

#### New features
NA

#### Bugs fixed
NA


### 20240313.v1

#### New features
NA

#### Bugs fixed
- Fix an issue where calling a flow with a flow function would result in failure.
- Improve error handling by categorizing errors as user errors when a run is archived prior to being processed by the runtime.


### 20240306.v5

#### New features
- Support "seed" parameter for built-in LLM tools and GPT-4V tools.

#### Bugs fixed
- Handle ClientAuthenticationError properly.
- Fix appending blob exceeded size limit error by truncating debug info.


### 20240228.v3

#### New features
- Support async flow test for long running jobs.

#### Bugs fixed
- Fix bug when collecting package tools.


### 20240222.v3

#### New features
- Added support for executing C# batch runs in eager mode.
- Introduced the ability to specify the number of workers for batch runs.
- Implemented functionality to define a timeout for batch runs.

#### Bugs fixed
NA

### 20240205.v2

#### New features
NA

#### Bugs fixed
- Fix the bug that deployed promptflow endpoint fails to get user assigned identity token.

### 20240124.v3

#### New features
- Support downloading data from Azure Machine Learning registry for batch run.
- Show node status when one line of a batch run times out.

#### Bugs fixed
- Fix the bug that exception raised during preparing data is not set in run history.
- Fix the bug that unexpected exception is raised when executor process crushes.

### 20240116.v1

#### New features
NA

#### Bugs fixed
- Add validation for wrong connection type for LLM tool.

### 20240111.v2

#### New features
- Support error log scrubbing for heron jobs.

#### Bugs fixed
- Fixed the compatibility issue between runtime and promptflow package < 1.3.0
