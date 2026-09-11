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

class Pricing
  attr_accessor :rule
  def initialize(rule) = @rule = rule
  def quote(base)
    raise ArgumentError, 'base' if base.negative?
    @rule.call(base)
  end
end

def discount(amount) = ->(base) { [0, base - amount].max }

pricing = Pricing.new(discount(10)); check(pricing.quote(100) == 90)
pricing.rule = discount(20)
check(pricing.quote(100) == 80 && pricing.quote(5).zero?)
expect_error { pricing.quote(-1) }
puts "OK strategy"
