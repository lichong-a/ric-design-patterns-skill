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

Style = Struct.new(:font)
Glyph = Struct.new(:character, :x, :style)
class StylePool
  def initialize = @cache = {}
  def get(font)
    @cache[font] ||= Style.new(font.dup.freeze).freeze
  end
end

pool = StylePool.new
a = Glyph.new('a', 1, pool.get('mono'))
b = Glyph.new('b', 8, pool.get('mono'))
check(a.style.equal?(b.style) && a.x != b.x)
check(!pool.get('serif').equal?(a.style))
puts "OK flyweight"
