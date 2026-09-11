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

TextNode = Struct.new(:value) do
  def accept(visitor) = visitor.visit_text(self)
end
NumberNode = Struct.new(:value) do
  def accept(visitor) = visitor.visit_number(self)
end
class RenderVisitor
  def visit_text(node) = "text:#{node.value}"
  def visit_number(node) = "number:#{node.value}"
end

visitor = RenderVisitor.new
check(TextNode.new('a').accept(visitor) == 'text:a')
check(NumberNode.new(7).accept(visitor) == 'number:7')
puts "OK visitor"
