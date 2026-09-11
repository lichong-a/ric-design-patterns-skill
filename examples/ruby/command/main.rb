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

Counter = Struct.new(:value)
class AddCommand
  def initialize(counter, delta)
    @counter, @delta, @phase = counter, delta, :new
  end
  def execute
    raise ArgumentError, 'execute once' unless @phase == :new
    @before = @counter.value
    @counter.value += @delta
    @phase = :done
  end
  def undo
    raise ArgumentError, 'nothing to undo' unless @phase == :done
    @counter.value = @before
    @phase = :undone
  end
end

counter = Counter.new(0)
command = AddCommand.new(counter, 3)
expect_error { command.undo }
command.execute; check(counter.value == 3)
expect_error { command.execute }
command.undo; check(counter.value.zero?)
expect_error { command.undo }
puts "OK command"
