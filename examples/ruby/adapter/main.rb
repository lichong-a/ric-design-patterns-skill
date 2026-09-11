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

class LegacySensor
  def centimeters = 250
end
class SensorAdapter
  def initialize(sensor) = @sensor = sensor
  def meters = @sensor.centimeters / 100.0
end

reader = SensorAdapter.new(LegacySensor.new)
check(reader.meters == 2.5)
puts "OK adapter"
