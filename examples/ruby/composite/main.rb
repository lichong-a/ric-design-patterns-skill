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

class LineItem
  def initialize(price)
    raise ArgumentError, 'price' if price.negative?
    @price = price
  end
  def total = @price
end
class Bundle
  def initialize(children) = @children = children.dup.freeze
  def total = @children.sum(&:total)
end

root = Bundle.new([LineItem.new(10), Bundle.new([LineItem.new(20), LineItem.new(30)])])
check(root.total == 60)
check(Bundle.new([]).total == 0)
expect_error { LineItem.new(-1) }
puts "OK composite"
