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

class Bag
  include Enumerable
  def initialize(values) = @values = values.dup.freeze
  def each
    return enum_for(:each) unless block_given?
    @values.each { |value| yield value }
    self
  end
end

bag = Bag.new([1, 2, 3])
a, b = bag.each, bag.each
check(a.next == 1 && a.next == 2 && b.next == 1)
check(bag.sum == 6 && bag.map { |n| n * 2 } == [2, 4, 6])
check(Bag.new([]).to_a == [])
puts "OK iterator"
