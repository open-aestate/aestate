import com.intellij.database.model.DasTable
import com.intellij.database.util.Case
import com.intellij.database.util.DasUtil

/*
 你可以使用此脚本快捷生成POJO对象
    最终效果为：
        from CACodeFramework.MainWork.CACodePojo import POJO


        class table(POJO):
            def __init__(self):
                self.shopId = None
                self.title = None
                self.icon = None
                self.createTime = None
                self.updateTime = None

 */

FILES.chooseDirectoryAndSave("Choose directory", "Choose where to store generated files") { dir ->
  SELECTION.filter { it instanceof DasTable }.each { generate(it, dir) }
}

def generate(table, dir) {
  def className = javaName(table.getName(), false)
  def fields = calcFields(table)
  new File(dir, className + ".py").withPrintWriter { out -> generate(out, className, fields) }
}

def generate(out, className, fields) {
  out.println "from CACodeFramework.MainWork.CACodePojo import POJO"
  out.println ""
  out.println ""
  out.println "class table(POJO):"
  out.println "    def __init__(self):"
  fields.each() {
    out.println "        self.${it.name} = None"
  }
}

def calcFields(table) {
  DasUtil.getColumns(table).reduce([]) { fields, col ->
    def spec = Case.LOWER.apply(col.getDataType().getSpecification())
    fields += [[
                 name : javaName(col.getName(), false)]]
  }
}

def javaName(str, capitalize) {
  def s = com.intellij.psi.codeStyle.NameUtil.splitNameIntoWords(str)
    .collect { Case.LOWER.apply(it).capitalize() }
    .join("")
    .replaceAll(/[^\p{javaJavaIdentifierPart}[_]]/, "_")
  capitalize || s.length() == 1? s : Case.LOWER.apply(s[0]) + s[1..-1]
}
