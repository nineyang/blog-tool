## 前言

`MySql`的`binlog`一般用于我们对数据的恢复，以及从数据库对主数据库的复制和更新。  
假设此时我们有一个需要查询和读取`Mysql`最近操作`DDL`的信息，我们需要怎么处理？  
聪明的你可能已经想到了，我们可以使用`mysqlbinlog`工具读取啊！的确，`mysqlbinlog`对于`statement`或者`mixed`格式的`binlog`文件确实会很方便读取，但是你要知道，从`Mysql5.7.7`开始，`row`就是默认的`binlog_format`，此时我们再要去直接通过肉眼去看，恐怕就不是那么容易了。

![d9630274-0be7-465a-8a0d-46dbe3d2441a.png](https://github.com/nineyang/blog-tool/blob/master/images/d9630274-0be7-465a-8a0d-46dbe3d2441a.png)

即使我们在通过`mysqlbinlog`解析时加上`-v`参数，也只能显示出这样的效果:

![f764edef-7cbd-421a-a6ea-d468aa803353.png](https://github.com/nineyang/blog-tool/blob/master/images/f764edef-7cbd-421a-a6ea-d468aa803353.png)

于是，我写了一个[binlog2sql](https://github.com/nineyang/binlog2sql)的初级版本，来实现`sql`语句的转换。

## 实现

实现过程不是很复杂，主要是通过`mysqlbinlog`来提取我们需要的`DDL`语句，然后我们再通过我们的方法来把这些语句转化为我们可以识别的`sql`语句。

核心代码:

    
    
    /**
         * @return $this
         */
        protected function selectFromBinLog()
        {
            $fillFile = Util::getFile(__DIR__ . '/data/file.sql');
            file_put_contents($fillFile, "");
            exec("mysqlbinlog -v --database='" . Conf::__DATABASE__ . "' $this->_binlog_basename/$this->_binlog_file | grep -E -i '###|UPDATE|INSERT|DELETE' >> $fillFile");
            return $this;
        }
    
        /**
         * @return $this
         */
        protected function parseSql()
        {
            $fillFileHandler = fopen(__DIR__ . '/data/file.sql', 'r');
            $sqlArr = [];
            if ($this->_type == 'ROW') {
                $match = NULL;
                $sqlStr = "";
                while (($sql = fgets($fillFileHandler)) !== false) {
                    if (($match = preg_match('/UPDATE|INSERT|DELETE/', $sql)) || strrpos($sql, 'end_log_pos') !== false) {
                        # 如果有指定表
                        if ($match && $this->_table && strpos($sql, $this->_table) === false) continue;
                        $sqlStr == '' || array_push($sqlArr, $sqlStr);
                        $sqlStr = $match ? trim(substr($sql, 3, -1)) . " " : "";
                    } elseif (strpos($sql, '@') !== false || strpos($sql, 'SET')) {
                        $sqlStr .= trim(substr($sql, 3, -1)) . " ";
                    }
                }
                $sqlStr == '' || array_push($sqlArr, $sqlStr);
            } else {
                # statement 和 mixed格式一样
                while (($sql = fgets($fillFileHandler)) !== false) {
                    $sql = trim($sql);
                    if (preg_match('/(UPDATE|INSERT|DELETE)\s+/', $sql)) {
                        array_push($sqlArr, $sql);
                    }
                }
            }
            $sqlArr = array_map(function ($value) {
                return preg_replace_callback('/(@(\d+))/', function ($matches) use ($value) {
                    $parts = explode('.', $value);
                    return $this->getTableColumns(explode('`', array_pop($parts))[1])[$matches[2] - 1];
                }, $value);
            }, $sqlArr);
    
            $mysqlFile = Util::getFile(__DIR__ . '/data/mysql.sql');
    
            array_map(function ($value) use ($mysqlFile) {
                file_put_contents($mysqlFile, $value . PHP_EOL, FILE_APPEND);
            }, $sqlArr);
            fclose($fillFileHandler);
    
            return $this;
        }
    
        /**
         * @param $table
         * @return array
         */
        protected function getTableColumns($table)
        {
            if (array_key_exists($table, $this->_tableColumns))
                return $this->_tableColumns[$table];
            $tableInfo = $this->select("show full columns from $table");
            if (empty($tableInfo)) Util::dd("$table 不存在");
            return $this->_tableColumns[$table] = array_column($tableInfo, 'Field');
        }

其中有三个主要的方法，`selectFromBinLog`用于执行`mysqlbinlog`，用于提取我们所需要的`DDL`，`parseSql`用于解析我们提取出来的`sql`，`getTableColumns`用于获取表的字段(主要是针对`row`模式下的`@1,@2`之类)。

当我们执行`Binlog.php`的`start`方法之后，就可以把`DDL`写入到'./data/mysql.sql'中了，非常方便。

![99b20b6e-d44e-4838-9827-e7c02d3fd69e.png](https://github.com/nineyang/blog-tool/blob/master/images/99b20b6e-d44e-4838-9827-e7c02d3fd69e.png)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:48 pm

