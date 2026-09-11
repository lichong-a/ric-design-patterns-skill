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

class Events
  def initialize
    @sequence, @listeners = 0, {}
  end
  def subscribe(&listener)
    raise ArgumentError, 'listener required' unless listener
    @sequence += 1
    @listeners[@sequence] = listener
    @sequence
  end
  def unsubscribe(token) = @listeners.delete(token)
  def emit(value) = @listeners.values.each { |listener| listener.call(value) }
end

events, seen = Events.new, []
token = events.subscribe { |n| seen << n }
events.emit(1); events.unsubscribe(token); events.emit(2)
check(seen == [1])
self_token = nil
self_token = events.subscribe { |_n| events.unsubscribe(self_token) }
events.emit(3); events.emit(4)
puts "OK observer"
