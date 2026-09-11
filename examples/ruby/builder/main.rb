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

Report = Struct.new(:title, :sections, keyword_init: true)
class ReportBuilder
  def initialize
    @title = ''
    @sections = []
  end
  def title(value)
    @title = value.strip
    self
  end
  def section(value)
    @sections << value.dup
    self
  end
  def build
    raise ArgumentError, 'title required' if @title.empty?
    Report.new(title: @title.dup.freeze, sections: @sections.map { |s| s.dup.freeze }.freeze).freeze
  end
end

builder = ReportBuilder.new
expect_error { builder.build }
first = builder.title('Design').section('Intent').build
builder.section('Tests')
check(first.sections == ['Intent'] && builder.build.sections.length == 2)
expect_error { first.sections << 'mutate' }
puts "OK builder"
