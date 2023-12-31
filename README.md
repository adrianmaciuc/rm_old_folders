# rm old folders

> A script designed as helper for [this yaml](https://github.com/adrianmaciuc/playwright-example-with-typescript/blob/main/.github/workflows/playwright.yml) 


## Usage

Script can be either downloaded using wget/curl or other tools during run commands in a github workflow. [Download link here](https://raw.githubusercontent.com/adrianmaciuc/rm_old_folders/main/rm_old_folders.py) 


```yaml
run: curl -LJO https://raw.githubusercontent.com/adrianmaciuc/rm_old_folders/main/rm_old_folders.py
```

Or you can put the the `rm_old_folders.py` file in the root of your repo. Then access it inside your steps

```yaml
run: python rm_old_folders.py --n-days 3 --folder-name .

```

> **Note**  
> Remember to install python first in your machine before running the script. You can easily use `actions/setup-python@v4`

## Params
The script takes mandatory two arguments:
`--n-days` - Number of days to determine which folders to delete. 
- Example: `--n-days 3` will delete all folders older than 3 days


`--folder-name` - Folder where the reports are, if the reports are at root, then type `.` (dot) 
- Example: `--folder-name .` will delete all folders from root of the repo
- Example2: `--folder-name reports` will delete all folders from `reports` directory of your repo

## Important details about the script logic

- Script searches for folders using this regex r'^\d{8}_\d{6}Z$' which will match with this timestamp format `%Y%m%d_%H%M%SZ` 
- Good Example: `20231129_000203Z`
- Bad Examples: that will be ignored: `whatever_text` `02528502520852` `reports 20231129_000203Z` 

> **Note**  
> Remember it must match the exact format `%Y%m%d_%H%M%SZ`` start till end, length included.
> For all other scenarios a message will be printed in the console that folder/file is skipped