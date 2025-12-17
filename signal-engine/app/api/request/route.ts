import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { title, description, category, priority, contact_email } = body;

    // Validate required fields
    if (!title || !description || !category || !priority) {
      return NextResponse.json(
        { error: 'Missing required fields: title, description, category, priority' },
        { status: 400 }
      );
    }

    // Validate priority
    if (!['low', 'medium', 'high'].includes(priority)) {
      return NextResponse.json(
        { error: 'Invalid priority. Must be: low, medium, or high' },
        { status: 400 }
      );
    }

    // Validate email if provided
    if (contact_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact_email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      );
    }

    // Prepare request data
    const requestData = {
      title: title.trim(),
      description: description.trim(),
      category: category.trim(),
      priority,
      contact_email: contact_email?.trim() || null,
      status: 'submitted',
      created_at: new Date().toISOString(),
      user_agent: request.headers.get('user-agent'),
      ip_address: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip'),
      request_id: `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    };

    // Try to insert into Supabase if configured
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (supabaseUrl && supabaseServiceKey) {
      try {
        const response = await fetch(`${supabaseUrl}/rest/v1/feature_requests`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${supabaseServiceKey}`,
            'apikey': supabaseServiceKey,
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          throw new Error(`Supabase error: ${response.status}`);
        }

        return NextResponse.json({ 
          success: true, 
          request_id: requestData.request_id,
          stored: 'supabase' 
        });
      } catch (supabaseError) {
        console.error('Supabase storage failed:', supabaseError);
        // Fall through to console logging
      }
    }

    // Fallback to console logging
    console.log('[FEATURE REQUEST]', JSON.stringify(requestData, null, 2));

    return NextResponse.json({ 
      success: true, 
      request_id: requestData.request_id,
      stored: 'console' 
    });
  } catch (error) {
    console.error('Feature request error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Only allow POST requests
export async function GET() {
  return NextResponse.json(
    { error: 'Method not allowed' },
    { status: 405 }
  );
}