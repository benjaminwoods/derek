import { Parser } from './parse.js'

class Derek {
  constructor(parent=null, children=null, value=null, name=null) {
    this.parent = parent
    this.children = children
    this.value = value
    this.name = name
  }

  get parser() {
    return Parser
  }

  static tree(obj, parent=null, name=null) {
    // TODO: return DerekTree (a subclass of Derek) instead of Derek.
    let children
    const self = new this()

    if (obj instanceof Array) {
      // Make child nodes
      children = obj.map(item => this.tree(item, self))
    } else if (obj instanceof Object) {
      // Make child nodes
      children = Object.values(obj).map(item => this.tree(item, self))
    } else {
      // Not iterable
      children = null
    }

    self.parent = parent
    self.children = children
    self.value = obj
    self.name = name

    return self
  }

  parse(format="oas3") {
    let parser, result

    format = format.toLowerCase()

    if (typeof this.parser[format] == "undefined") {
      throw "Not yet supported."
    }

    result = this.parser[format](this)
    result.example = this.example()

    return {
      [this.name || "untitled"]: result
    }
  }

  example() {
    let result;
    if (this.value.constructor == Array) {
      if (this.value.length == 0) {
        result = []
      } else {
        let c, v;

        c = this.children[0]
        v = c.example()
        result = [c instanceof Derek ? c.example() : c]
      }
    } else if (this.value.constructor == Object) {
      if (Object.keys(this.value).length == 0) {
        result = {}
      } else {
        let keys, values;
        keys = Object.keys(this.value),
        values = this.children.map(
          c => c instanceof Derek ? c.example() : c
        )

        result = Object.fromEntries(
          keys.map((e,i) => [e,values[i]])
        )
      }
    } else {
      result = JSON.parse(JSON.stringify(this.value))
    }

    return result
  }
}

export { Derek };
