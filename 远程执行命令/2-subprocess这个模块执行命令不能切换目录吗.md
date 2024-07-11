subprocess这个模块执行命令不能切换目录吗

您提出了一个很好的问题。`subprocess` 模块确实可以执行命令,但是它无法直接切换当前工作目录。

这是因为 `subprocess` 模块是用来执行外部程序的,而不是直接操作 Python 解释器的当前工作目录。当您在 Python 代码中使用 `subprocess.check_output()` 执行 `cd` 命令时,它只是在子进程中执行了 `cd` 命令,但并不会影响 Python 解释器本身的工作目录。

如果您想在 Python 代码中切换当前工作目录,可以使用 `os.chdir()` 函数:

```python
import os

def Cmd(cmd_text):
    try:
        # 切换到目标目录
        os.chdir('/root/pythontest/remote_cmd')
        
        # 执行命令
        out_res = subprocess.check_output(cmd_text, shell=True, universal_newlines=True)
        err_res = ''
        data_size = len(out_res.encode('utf-8'))
        print(f"Command output: {out_res}")
        return out_res, err_res, data_size
    except subprocess.CalledProcessError as e:
        # 命令执行出错
        out_res = ''
        err_res = f"Error executing command: {e}"
        data_size = len(err_res.encode('utf-8'))
        print(f"Command error: {err_res}")
        return out_res, err_res, data_size
    except Exception as e:
        # 其他异常
        out_res = ''
        err_res = f"Unexpected error: {e}"
        data_size = len(err_res.encode('utf-8'))
        print(f"Unexpected error: {err_res}")
        return out_res, err_res, data_size
```

在这个例子中,我们先使用 `os.chdir()` 函数切换到目标目录 `/root/pythontest/remote_cmd`，然后再执行命令。这样就可以确保命令在正确的目录下执行。

需要注意的是,`os.chdir()` 函数只会影响当前 Python 进程的工作目录,不会影响其他进程或者子进程。所以在执行完命令后,可能需要再次切换回原来的工作目录。

总之,如果您需要在 Python 代码中切换工作目录,可以使用 `os.chdir()` 函数来实现。