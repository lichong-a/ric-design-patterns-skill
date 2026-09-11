# frozen_string_literal: true

def check(condition)
  raise 'check failed' unless condition
end

def expect_error
  failed = false
  begin
    yield
  rescue StandardError
    failed = true
  end
  check(failed)
end

class Literal
  def initialize(value) = @value = value
  def evaluate(_context) = @value
end
class Variable
  def initialize(name) = @name = name
  def evaluate(context) = context.fetch(@name)
end
class Add
  def initialize(left, right)
    @left, @right = left, right
  end
  def evaluate(context) = @left.evaluate(context) + @right.evaluate(context)
end

expr = Add.new(Variable.new('x'), Literal.new(2))
check(expr.evaluate('x' => 3) == 5)
expect_error { expr.evaluate({}) }
puts "OK interpreter"
