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

class RealImage
  def read = 'pixels'
end
class LazyImage
  attr_reader :loads
  def initialize
    @real = nil
    @loads = 0
  end
  def read
    unless @real
      @real = RealImage.new
      @loads += 1
    end
    @real.read
  end
end

image = LazyImage.new
check(image.loads.zero?)
check(image.read == 'pixels' && image.read == 'pixels')
check(image.loads == 1)
puts "OK proxy"
