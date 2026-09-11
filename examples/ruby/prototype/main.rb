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

class Document
  attr_accessor :title, :paragraphs
  def initialize(title, paragraphs)
    @title = title
    @paragraphs = paragraphs
  end
  def initialize_copy(other)
    super
    @title = other.title.dup
    @paragraphs = other.paragraphs.map { |row| row.map(&:dup) }
  end
end

original = Document.new('Design', [['one']])
copied = original.dup
copied.paragraphs[0][0].replace('changed')
copied.paragraphs[0] << 'two'
check(original.paragraphs == [['one']])
check(copied.paragraphs[0].length == 2)
puts "OK prototype"
