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

class Snapshot
  def initialize(owner, text)
    @owner, @text = owner, text.dup.freeze
    freeze
  end
  def read_for(owner)
    raise ArgumentError, 'foreign snapshot' unless @owner.equal?(owner)
    @text
  end
end
class Editor
  attr_accessor :text
  def initialize
    @owner, @text = Object.new.freeze, ''
  end
  def initialize_copy(_other) = raise(TypeError, 'editor identity cannot be copied')
  def save = Snapshot.new(@owner, @text)
  def restore(snapshot) = @text = snapshot.read_for(@owner).dup
end

a, b = Editor.new, Editor.new
a.text = 'one'; saved = a.save; a.text = 'two'
a.restore(saved); check(a.text == 'one')
a.text.replace('edited'); a.restore(saved); check(a.text == 'one')
expect_error { b.restore(saved) }
puts "OK memento"
