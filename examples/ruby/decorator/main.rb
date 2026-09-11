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

class PlainText
  def render = 'hi'
end
class PrefixText
  def initialize(inner) = @inner = inner
  def render = "!#{@inner.render}"
end
class BracketText
  def initialize(inner) = @inner = inner
  def render = "[#{@inner.render}]"
end

check(BracketText.new(PrefixText.new(PlainText.new)).render == '[!hi]')
check(PrefixText.new(BracketText.new(PlainText.new)).render == '![hi]')
puts "OK decorator"
