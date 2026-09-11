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

class Rule
  def initialize(accepts, next_rule = nil)
    @accepts, @next_rule = accepts, next_rule
  end
  def handle(value)
    @accepts.call(value) && (@next_rule.nil? || @next_rule.handle(value))
  end
end

visits = 0
chain = Rule.new(->(n) { n.positive? }, Rule.new(->(n) { visits += 1; n < 10 }))
check(!chain.handle(-1) && visits.zero?)
check(chain.handle(5) && visits == 1)
check(!chain.handle(12) && visits == 2)
puts "OK chain-of-responsibility"
